% order5v2_0458  eq1=40603 eq2=24303  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,f(Z,W)),W),Z),U) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,X),Z),f(f(Z,X),W)) )).
