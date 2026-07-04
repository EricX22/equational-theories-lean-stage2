% order5_0069  eq1=58584 eq2=20590  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( f(f(X,Y),Y) = f(Y,f(X,f(X,Y))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,Y),f(f(f(Y,Z),X),X)) )).
