% hard3_0229  eq1=2093 eq2=1890  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,X),X),f(Z,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(X,X)),f(Z,X)) )).
