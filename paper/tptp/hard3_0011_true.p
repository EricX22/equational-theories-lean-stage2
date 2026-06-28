% hard3_0011  eq1=51 eq2=2862  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(X,f(Y,Z))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(X,f(Y,X)),X),X) )).
