% hard3_0391  eq1=4392 eq2=4677  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,f(X,X)) = f(f(Y,Z),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(f(X,Y),Z) != f(f(Y,X),Z) )).
