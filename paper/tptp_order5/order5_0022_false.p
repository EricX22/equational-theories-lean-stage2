% order5_0022  eq1=53505 eq2=2965  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,Y) = f(f(f(f(Z,X),W),W),U) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,f(Y,Z)),Z),Y) )).
