% order5v2_0664  eq1=41399 eq2=18608  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(f(Y,Z),W),X),Z),Y) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(Y,Z),f(W,f(f(X,U),Z))) )).
