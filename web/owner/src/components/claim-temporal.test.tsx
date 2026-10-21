import {describe, it, expect} from 'vitest';
import {renderToStaticMarkup} from 'react-dom/server';
import {claimDisplayTitle} from './claim-display';
import {ClaimTemporal} from './claim-temporal';

describe('finding time presentation', () => {
  const qualifiers = {effective_date:'2026-10-15', report_date:'2026-10-19', historical_reconstruction:true};
  it('moves redundant title dates into explicit labels without altering the statement', () => {
    const claim = {title:'October 15 leverage snapshot described in October 19 report', statement:'The October 19 report describes October 15 positions.', qualifiers};
    expect(claimDisplayTitle(claim)).toBe('Leverage snapshot');
    expect(claim.statement).toContain('October 19');
    const html = renderToStaticMarkup(<ClaimTemporal claim={claim}/>);
    expect(html).toContain('Data as of'); expect(html).toContain('2026-10-15');
    expect(html).toContain('Report'); expect(html).toContain('2026-10-19');
    expect(html).toContain('first-known time unverified');
  });
  it('preserves comparison dates and unsupported legacy dates', () => {
    expect(claimDisplayTitle({title:'October 15–19 leverage change', qualifiers})).toBe('October 15–19 leverage change');
    expect(claimDisplayTitle({title:'October 15 leverage snapshot'})).toBe('October 15 leverage snapshot');
    expect(claimDisplayTitle({statement:'October 15 prices fell', qualifiers})).toBe('October 15 prices fell');
  });
  it('shows reconstruction and unknown availability even without dates', () => {
    const claim = {qualifiers:{historical_reconstruction:true}};
    const html = renderToStaticMarkup(<ClaimTemporal claim={claim}/>);
    expect(html).toContain('Historical reconstruction');
    expect(html).toContain('first-known time unverified');
    expect(renderToStaticMarkup(<ClaimTemporal claim={claim} compact/>)).toBe('');
  });
  it('does not present invalid calendar dates', () => {
    expect(renderToStaticMarkup(<ClaimTemporal claim={{qualifiers:{effective_date:'2026-02-30'}}}/>)).toBe('');
  });
  it('supports graph temporal projection and never labels created_at as observation time', () => {
    expect(renderToStaticMarkup(<ClaimTemporal claim={{temporal:{effective_date:'2026-10-15', recorded_at:'2026-10-20'}}}/>)).not.toContain('2026-10-20');
  });
});
