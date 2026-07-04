% order5v2_0750  eq1=18221 eq2=30389  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,Y),f(X,f(f(Y,Z),Y))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(X,f(f(Y,Z),X))),Y) )).
