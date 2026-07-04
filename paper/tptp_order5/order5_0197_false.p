% order5_0197  eq1=1269 eq2=26094  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(X,f(f(f(Y,Z),Z),W)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(Y,f(f(X,Z),W)),f(U,W)) )).
