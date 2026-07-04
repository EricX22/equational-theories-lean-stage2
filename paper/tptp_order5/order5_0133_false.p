% order5_0133  eq1=45411 eq2=29005  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(Y,f(f(f(X,Z),X),X)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(f(Y,Z),Y),Z),f(W,W)) )).
