% hard3_0208  eq1=1962 eq2=4175  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(Z,X)),f(Y,X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(f(Y,Z),X),Y) )).
