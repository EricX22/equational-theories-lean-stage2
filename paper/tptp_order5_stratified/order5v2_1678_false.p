% order5v2_1678  eq1=37564 eq2=37636  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,f(Y,f(Y,Z))),Z),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,f(Y,f(Z,W))),Z),W) )).
