% mbti_scores.pl
% ----------------
% This module turns a list of responses into an MBTI type string,
% correctly accounting for which side (E vs I, S vs N, etc.) each
% question favors.

:- module(mbti_scores, [calculate_mbti/2]).

% Map a user answer (1–5) to a contribution between -2 and +2
contribution(UserScore, Value) :-
    Value is UserScore - 3.

% calculate_mbti(+Responses, -MBTI)
%   Responses = [ resp(Dimension,Side,UserScore), ... ]
%   Dimension ∈ {e_i,s_n,t_f,j_p}; Side ∈ {e,i,s,n,t,f,j,p}
calculate_mbti(Responses, MBTI) :-
    dims([e_i, s_n, t_f, j_p]),
    maplist(sum_dimension(Responses), [e_i, s_n, t_f, j_p], [SumEI, SumSN, SumTF, SumJP]),
    ( SumEI >= 0 -> C1 = 'E' ; C1 = 'I' ),
    ( SumSN >= 0 -> C2 = 'S' ; C2 = 'N' ),
    ( SumTF >= 0 -> C3 = 'T' ; C3 = 'F' ),
    ( SumJP >= 0 -> C4 = 'J' ; C4 = 'P' ),
    string_concat(C1, C2, P12),
    string_concat(P12, C3, P123),
    string_concat(P123, C4, MBTI).

% The four MBTI dimensions we consider
dims([e_i, s_n, t_f, j_p]).

% sum_dimension(+Responses, +Dim, -Sum)
%   Sums each response’s contribution, flipping sign when Side is the second pole.
sum_dimension(Responses, Dim, Sum) :-
    findall(Val, (
        member(resp(Dim, Side, Score), Responses),
        contribution(Score, RawVal),
        % Flip if this question’s “positive” side is the second letter
        flip_if_needed(Dim, Side, RawVal, Val)
    ), Vals),
    sum_list(Vals, Sum).

% flip_if_needed(+Dim, +Side, +RawVal, -Val)
%   If Side is the “opposite” pole for this dimension, invert the contribution.
flip_if_needed(e_i, i, Raw, Val) :- Val is -Raw.
flip_if_needed(e_i, e, Raw, Val) :- Val = Raw.

flip_if_needed(s_n, n, Raw, Val) :- Val is -Raw.
flip_if_needed(s_n, s, Raw, Val) :- Val = Raw.

flip_if_needed(t_f, f, Raw, Val) :- Val is -Raw.
flip_if_needed(t_f, t, Raw, Val) :- Val = Raw.

flip_if_needed(j_p, p, Raw, Val) :- Val is -Raw.
flip_if_needed(j_p, j, Raw, Val) :- Val = Raw.
